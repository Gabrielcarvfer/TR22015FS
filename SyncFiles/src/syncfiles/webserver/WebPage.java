/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package syncfiles.webserver;

import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Gustavo
 */
public class WebPage {
    String userName = null;
    
     public WebPage(String httpContent) throws Exception {
         setUsername(httpContent);
         updatePage();
     }

    private void setUsername(String httpContent){
       userName = httpContent.substring(5);   
    }

    public void updatePage(){
    PrintWriter writer = null;
        try {
            writer = new PrintWriter("webpage/mainpage.html", "UTF-8");
            writer.println("<!DOCTYPE html>");
            writer.println("<html>");
            writer.println("<head> Bem vindo,"+userName+ "!</head>");
            writer.println("<body></body>");
            writer.println("</html>");
            writer.close();
        } catch (FileNotFoundException ex) {
            Logger.getLogger(WebPage.class.getName()).log(Level.SEVERE, null, ex);
        } catch (UnsupportedEncodingException ex) {
            Logger.getLogger(WebPage.class.getName()).log(Level.SEVERE, null, ex);
        } finally {
            writer.close();
        }
    
    
    }
    
    
    public void printUsername(){
    System.out.print(userName);
    }
    
}
