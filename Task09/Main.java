import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;


public class Main
{
    public enum State {
        GROUP_BODY, GARBAGE, ESCAPED_CHAR,
    }

    public static void main(String[] args)
    {

        FileInputStream in = null;
        
        try
        {
            in = new FileInputStream("data.txt");
            int c;
            State state = State.GROUP_BODY;
            int level = 0;
            int score = 0;
            
            
            while ((c = in.read()) != -1) {
                switch(state) {
                    case GARBAGE:
                        switch(c) {
                            case '!':
                                state = State.ESCAPED_CHAR;
                            break;
                            case '>':
                                state = State.GROUP_BODY;
                            break;
                        }
                    break;
                
                    case GROUP_BODY:
                        switch(c) {
                            case '{':
                                level++;
                                score += level;
                            break;
                            case '}':
                                level--;
                            break;
                            
                            case '<':
                                state = State.GARBAGE;
                            break;
                        }
                    break;
                    
                    case ESCAPED_CHAR:
                        state = State.GARBAGE;
                    break;
                }
            }

            in.close();

            System.out.format("Done! Score: %d\n", score);

        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }
}
