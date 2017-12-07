#!/usr/bin/env scala
import scala.io.Source
import java.io.FileNotFoundException
import java.io.IOException
import scala.collection.mutable.ListBuffer
import scala.util.control.Breaks._


object HelloWorld {
  val filename = "data.txt"

  def main(args: Array[String]): Unit = {
    var parents = Map[String, String]();
    var parent_key = "";
    var child_key = "";
    
    // Fill in a child-to-parent map
    for (line <- Source.fromFile(filename).getLines) {
        var items = line.split(" ")
        parent_key = items.apply(0)
        
        for(child <- items.slice(3, items.length)) {
            if(child.endsWith(",")) { 
              child_key = child.slice(0, child.length - 1)
            } else {
              child_key = child;
            }
            parents += (child_key -> parent_key)
        }
    }
    
    // Pick any node (parent_key), keep picking parents untill we reach the root.
    breakable {
        while(true) {
          if(!parents.contains(parent_key)) {
            // No parent, means it's root.
            println(parent_key)
            break;
          }
          parent_key = parents.apply(parent_key)
        }
    }
  }
}
