/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package syncfiles.peercomm;

import java.net.InetAddress;

/**
 *
 * @author gabriel
 */

  /*
    Peer info to be transmitted need the following parameters
    long time;
    InetAddress ip;
    byte [] mac;
    */
    
public class PeerInfo {
         long time;
         InetAddress ip;
         byte [] mac;
         
         PeerInfo(long time, InetAddress ip, byte[] mac)
         {
                  this.time = time;
                  this.ip = ip;
                  this.mac = mac;
         }
}
