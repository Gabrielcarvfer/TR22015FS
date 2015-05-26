package syncfiles.webserver;

import java.net.ServerSocket;
import java.net.Socket;

public class WebServer {

  /**
   * WebServer constructor.
   */

    public void start() {
        ServerSocket socket;

        System.out.println("Iniciando Webserver na porta 80");

        try {
          socket = new ServerSocket(80);
        } catch (Exception e) {
          System.out.println("Erro: " + e);
          return;
        }

        System.out.println("Esperando conexÃ£o...");
        for (;;) {
          try {
                // Listen for a TCP connection request.
                Socket connection = socket.accept();

                // Construct an object to process the HTTP request message.
                HttpRequest request = new HttpRequest(connection);

                // Create a new thread to process the request.
                Thread thread = new Thread(request);

                // Start the thread.
                thread.start();


          } catch (Exception e) {
            System.out.println("Erro: " + e);
          }
        }
  }
}
