/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package syncfiles.peercomm;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.nio.ByteBuffer;

/**
 *
 * @author gabriel
 */
public class ByteUtilities {
    private static ByteBuffer buffer = ByteBuffer.allocate(Long.BYTES);    

    public static synchronized byte[] longToBytes(long x) {
        buffer.putLong(0, x);
        return buffer.array();
    }

    public static synchronized long bytesToLong(byte[] bytes) {
        buffer.put(bytes, 0, bytes.length);
        buffer.flip();//need flip 
        return buffer.getLong();
    }
    
    public static synchronized byte[] buildAck() throws IOException
    {
         ByteArrayOutputStream sendData = new ByteArrayOutputStream (64);      
         
         //Sending local time, ip and mac address as ack
         long timestamp = System.currentTimeMillis();
         InetAddress localIP = InetAddress.getLocalHost();
        
         sendData.write(ByteUtilities.longToBytes(timestamp));
         sendData.write(localIP.getAddress());
         
         return sendData.toByteArray();
    }
    
    public static synchronized PeerInfo getPeerInfo (byte[] receivedPacket) throws IOException
    {
         ByteArrayOutputStream tempBuffer = new ByteArrayOutputStream (64);   
         
         tempBuffer.write(receivedPacket, 0, 4);
         long timestamp = ByteUtilities.bytesToLong(tempBuffer.toByteArray());
         tempBuffer.flush();
         
         tempBuffer.write(receivedPacket, 4, 4);
         InetAddress sourceIP = InetAddress.getByAddress(tempBuffer.toByteArray());
         tempBuffer.flush();
         
         byte[] MAC = NetworkInterface.getByInetAddress(sourceIP).getHardwareAddress();
         
         return new PeerInfo(timestamp, sourceIP, MAC);
    }
}
