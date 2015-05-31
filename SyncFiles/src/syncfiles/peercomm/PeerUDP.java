/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package syncfiles.peercomm;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketTimeoutException;
import java.util.Collection;

/**
 *
 * @author gabriel
 */
public class PeerUDP 
{
    private static final String broadcastIP = "255.255.255.255";
    private static final int    defaultUDPPort = 1234;
    private static final int packageSize = 64;
    private static final int timeout = 300; //milliseconds
   
      /**
    * Run UDP server. 
    * This function receives an UDP packet, retrieves the info sent and answer the 
    * packet sender with its peer info {@link PeerInfo} .
    * <p>
    *
    * @return PeerInfo original sender peer information
    * @throws java.io.IOException
    * @see    PeerUDP
    */
    public PeerInfo run_server () throws IOException
    {
         //Open UDP socket
         DatagramSocket serverSocket = new DatagramSocket(PeerUDP.defaultUDPPort);      
         
         //Set datagram sizes
         byte[] receiveData = new byte[packageSize];     
         byte[] sendData;
  
         //Receive package on port 1024
         DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);    
         serverSocket.receive(receivePacket);       
         PeerInfo peerInfo = ByteUtilities.getPeerInfo(receivePacket.getData());
        
         //Get IP source and answer correctly
         InetAddress sourceIP = receivePacket.getAddress();          
         int sourcePort = receivePacket.getPort();    
         sendData = ByteUtilities.buildAck();
    
         DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, sourceIP, sourcePort); 
         serverSocket.send(sendPacket);               
         return peerInfo;
    }
    
    
    /**
    * Run UDP client. 
    * This function broadcasts an UDP packet and retrieves the info
    * sent by peers that answered the request. {@link PeerInfo} .
    * <p>
    * The return is a collection of all UDP servers info that were sent in time.
    * 
    * @return Collection collection of peer information received
    * @throws java.io.IOException
    * @see    PeerUDP
    */
    public Collection<PeerInfo> run_client () throws IOException
    {
        //Allocate structures and address to send message
        InetAddress IPAddress = InetAddress.getByName(PeerUDP.broadcastIP);
        byte[] sendData = new byte[packageSize];      
        byte[] receiveData = new byte[packageSize];  
        DatagramSocket clientSocket = new DatagramSocket();
        
         //Set timeout
         clientSocket.setSoTimeout(timeout);
        
         //Copy message to datagram
         sendData = ByteUtilities.buildAck(); 
        
         //Prepare datagram
         DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, PeerUDP.defaultUDPPort);  
        
         //Send package
         clientSocket.send(sendPacket);   
         Collection<PeerInfo> peerInfo = null;
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
                peerInfo.add(ByteUtilities.getPeerInfo(receivePacket.getData()));

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
         return peerInfo;
    }
    
}
