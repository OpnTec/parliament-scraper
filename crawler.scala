

import akka.actor.{ActorSystem,Props,Actor}
import akka.event.Logging
import spray.client.pipelining._
import spray.http.{HttpRequest, HttpResponse}
import scala.concurrent.{future,Future}
import akka.pattern._
import scala.concurrent.ExecutionContext
import ExecutionContext.Implicits.global

case class PDF(url:String)
case class Page(id:Int)


object Main extends App{
  val lastPage = 50
  //change this line to determine how much you want to crawl
  implicit val system = ActorSystem("crawler-system")
  val crawler = system.actorOf(Props[PageRequestActor],"crawler")
  (1 to lastPage).foreach(crawler ! Page(_))
}

class DownloadActor extends Actor{
  import sys.process._
  import java.net.URL
  import java.io.File

  def fileDownloader(url: String, filename: String) = {
    new URL(url) #> new File(filename) !!
  }
  val fileNameExtractor = """.*\/(.*?.pdf)""".r
  val log = Logging(context.system,this)

  def receive = {
    case PDF(url) =>
      val fileNameExtractor(name) = url
      val file = Future{
        fileDownloader(url,name)
      }
      file onFailure{
        case e:Throwable => log.error(e,"error in downloading")
      }
      file onSuccess{
        case _ => log.info("new file download complete")
      }
  }
}

class PageRequestActor extends Actor{
  val baseURL = "http://www.europarl.europa.eu/RegistreWeb/search/typedoc.htm?codeTypeDocu=QECR&year=2015&lg=EN&currentPage="
  val parser = context.actorOf(Props[PageParserActor],"parser")
  def receive = {
    case Page(num) =>
      val pipeline: HttpRequest => Future[HttpResponse] = sendReceive
      val r = pipeline(Get(baseURL + num.toString))
      pipe(r) pipeTo parser
  }
}

class PageParserActor extends Actor{
  val log = Logging(context.system, this)
  val PDFextractor = """href="(http.*?\.pdf)"""".r

  val downloader = context.actorOf(Props[DownloadActor],"download-actor")
  def receive = {
    case response:HttpResponse =>
      if (response.status.isSuccess){
        val body = response.entity.asString
        val matches = PDFextractor
          .findAllMatchIn(body)
          .map(_.group(1))
          .foreach(downloader ! PDF(_))
      }
      else
        log.warning("Failed to parse one page")
    case e:Throwable => log.error(e,"Error in perform request")
  }
}
