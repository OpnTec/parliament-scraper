#!/usr/bin/env ruby

require 'bundler/setup'
require 'rubygems'

require 'net/http'
require 'nokogiri'
require 'open-uri'
require 'fileutils'

year = 2015
document_type = 'QECR'   # Parliamentary Written Questions
language = 'EN'   # Language => English

max_page_num = 1
current_page = 1

# Create docs/ directory if it doesn't exist
FileUtils::mkdir_p 'docs'

# Trap Ctrl-C/SIGINT signal
interrupted = false
trap("INT") { puts "Shutting Down!"; interrupted = true }

loop do
  uri = URI.parse("http://www.europarl.europa.eu/RegistreWeb/search/typedoc.htm?codeTypeDocu=#{document_type}&year=#{year}&lg=#{language}&currentPage=#{current_page}")
  response = Net::HTTP.get(uri)
  page = Nokogiri::HTML(response)

  # Update New Max Page Number
  max_page_num = page.css(".ep_paginate li a").last.attr("title").to_i

  # Get Links to Questions on the current page
  links = page.css(".results .notice .documents a").map { |record| record.attr("href") }

  # Download Files to docs/ directory
  links.each do |link|
    file_name = link.split('/').last
    File.open("docs/#{file_name}", "wb") do |f|
      f << open(link).read
    end

    # If Process has been interrupted or is completed, exit the program
    exit if interrupted
  end

  # If no more documents remain to be downloaded
  break if current_page == max_page_num
end

puts "Process Successfully Completed"
