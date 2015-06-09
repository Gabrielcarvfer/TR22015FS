/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package syncfiles.webserver;

import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.StringTokenizer;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Gustavo
 */
public class WebPage {
    String userName = null;
    PrintWriter writer = null;
    
     public WebPage(String httpContent) throws Exception {
         processContent(httpContent);
         updatePage();
     }

    private void processContent(String httpContent){
         if(httpContent.contains("user"))
        {
        userName = httpContent.substring(5);
        }
    }

    public void updatePage(){
   
        try {
            writer = new PrintWriter("webpage/mainpage.html", "UTF-8");
            writer.println("<!DOCTYPE html>");
            writer.println("<html>");
            writer.println("<head> Bem vindo,"+userName+ "!</head>");
            writer.println("<body>");
            writer.println("<div> <p>Criar novo diretório</p>");
            writer.println("<form  method=\"POST\" action=\"mainpage.html\">");
            writer.println("<p>Nome do pai do novo diretório:");
            writer.println("<select name=\"dir\">");
            printDir();
            writer.println("</select></p>");
            writer.println("<p>Nome do novo diretório:<input type=\"text\"name=\"dirName\"></p>");
            writer.println("<input type=\"submit\" value=\"Submit\">");
            writer.println("</form>");
            writer.println("</div>"); 
            
            writer.println("<div> <p>Adicionar arquivo</p>");
            writer.println("<p>Diretório onde o arquivo vai ser alocado:</p>");
            writer.println("<form  method=\"POST\" action=\"mainpage.html\">");
            writer.println("<select name=\"fileDir\">");
            writer.println("<option value=\"Arquivos\">Arquivos</option>");
            writer.println("</select></p>");
            writer.println("<p>Nome do novo diretório:<input type=\"text\"name=\"fileeName\"></p>");
            writer.println("<input type=\"submit\" value=\"Submit\">");
            writer.println("</form>");
            writer.println("</div>"); 
            
                       
            writer.println("</body>");
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
    
    private void printDir(){
     writer.println("<option value=\"nenhum\">Não desejo criar novo diretório</option>");
     writer.println("<option value=\"pai\">Arquivos</option>");
    
    }
    
    public void printUsername(){
    System.out.print(userName);
    }
    
}
