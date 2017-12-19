import java.io.File
import java.io.InputStream

 
fun main(args: Array<String>) {
	val inputStream: InputStream = File("data.txt").inputStream()
 
	val lineList = mutableListOf<String>()
    var links = HashMap<String, MutableSet<String>>()

    // Build a map {program: <list of linked programs>}
	inputStream.bufferedReader().useLines { lines -> lines.forEach { lineList.add(it)} }
	lineList.forEach{
        val items = it.split(" <-> ")
        val program1 = items[0]
        
        links.set(program1, mutableSetOf<String>())
        
        items[1].split(", ").forEach{
            links.get(program1)!!.add(it)
            
            if (!links.contains(it)) {
                links.set(it, mutableSetOf<String>())
            }
            links.get(it)!!.add(program1)
        }
    }
    
    // Do a DFS, keeping unique programs in `found`
    var found = mutableSetOf<String>()
    var pending = mutableListOf("0")
    
    while (pending.isNotEmpty()) {
        val program = pending.removeAt(pending.size - 1)
        found.add(program)

        links.get(program)!!.forEach {
            if (!found.contains(it)) {
                pending.add(it)
            }
        }        
    }
    print(found.size)
    print("\n")
}
