name := "parliment_crawler"
version := "0.1"
scalaVersion := "2.11.7"
resolvers += "spray repo" at "http://repo.spray.io"
//spray stack
libraryDependencies ++= {
  val akkaV = "2.4.1"
  val sprayV = "1.3.3"
  Seq(
    "io.spray" %% "spray-client" % sprayV,
    "com.typesafe.akka" %% "akka-actor" % akkaV
  )
}
