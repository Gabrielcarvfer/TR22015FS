/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package syncfiles.peercomm;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketTimeoutException;

/**
 *
 * @author gabriel
 */
public class PeerUDP 
{
    private static String broadcastIP = "255.255.255.255";
    private static int    defaultUDPPort = 1234;
   
    /*
    Peer info to be transmitted need the following parameters
    long time;
    InetAddress ip;
    byte [] mac;
    int port;
    */
    
    void run_server () throws IOException
    {
        DatagramSocket serverSocket = new DatagramSocket(PeerUDP.defaultUDPPort);           
        byte[] receiveData = new byte[1024];     
        byte[] sendData = new byte[1024];           
  
        //Receive package on port 1024
        DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);    
        serverSocket.receive(receivePacket);         
        String sentence = new String( receivePacket.getData());  
        //System.out.println("RECEIVED: " + sentence);  
        
        //Get IP source and answer correctly
        InetAddress IPAddress = receivePacket.getAddress();          
        int port = receivePacket.getPort();    
            
        //return localhost data as ack
        String capitalizedSentence = sentence.toUpperCase(); 
        sendData = capitalizedSentence.getBytes();              
        DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, port); 
        serverSocket.send(sendPacket);               
    }
    
    void run_client () throws IOException
    {
        //Allocate structures and address to send message
        InetAddress IPAddress = InetAddress.getByName(PeerUDP.broadcastIP);
        byte[] sendData = new byte[1024];      
        byte[] receiveData = new byte[1024]; 
        
        //Input message to send
        BufferedReader inFromUser = new BufferedReader(new InputStreamReader(System.in));    
        DatagramSocket clientSocket = new DatagramSocket();
        clientSocket.setSoTimeout(300);
        String sentence = inFromUser.readLine();  
        
        //Copy message to datagram
        sendData = sentence.getBytes(); 
        
        //Prepare datagram
        DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, PeerUDP.defaultUDPPort);  
        
        //Send package
        clientSocket.send(sendPacket);   
        
        while(true)
        {
            /*
            Try to receive multiple packets, in case of more than one 
              peer listened and awnsered in time
            */
            try
            {
                //Receive acknowledge package with data 
                DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);    
                clientSocket.receive(receivePacket); 
                InetAddress sourceIPAddress = receivePacket.getAddress();
                String modifiedSentence = new String(receivePacket.getData());

                //Return ack to source IP
                sendPacket = new DatagramPacket(sendData, sendData.length, sourceIPAddress, PeerUDP.defaultUDPPort);
                clientSocket.send(sendPacket);
            } 
            catch (SocketTimeoutException ex)
            {
                break;
            }
        }
        //System.out.println("FROM SERVER:" + modifiedSentence);    
        clientSocket.close();    
    }
    
    
    void getInfo()
    {
    
    }
    
    void sendInfo()
    {
        
    }
}
