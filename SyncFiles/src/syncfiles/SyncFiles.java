/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package syncfiles;

import java.io.File;
import static java.lang.Thread.sleep;
import java.net.UnknownHostException;
import syncfiles.filesystem.FileSystem;
import syncfiles.webserver.WebServer;

/**
 *
 * @author Gabriel
 */
public class SyncFiles {

    /**
     * @param args the command line arguments
     * @throws java.lang.InterruptedException
     * @throws java.net.UnknownHostException
     */
    public static void main(String[] args) throws InterruptedException, UnknownHostException 
    {       
       //Cria árvore que percorre arquivos e pastas
<<<<<<< HEAD
        //File file = new File(System.getProperty("user.dir")); 
        //FileSystem fs = new FileSystem();
        //fs.reIndexFolder(file);
        
        WebServer ws = new WebServer();
        ws.start();
=======
       // File file = new File(System.getProperty("user.dir")); 
        //FileSystem fs = new FileSystem();
       // fs.reIndexFolder(file);
        
       WebServer ws = new WebServer();
       ws.start();
>>>>>>> be49970f6cdae092eac7d1592010460deff6ef75
        
       System.out.println("Esperando pra acabar"); 
        sleep(10000);
        
        
    }
    
   
}
