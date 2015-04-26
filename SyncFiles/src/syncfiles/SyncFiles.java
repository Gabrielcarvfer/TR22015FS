/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package syncfiles;

import java.io.File;
import java.sql.Connection;
import java.util.ArrayList;
import java.util.Collection;
import syncfiles.dao.DBConnectionManager;
import syncfiles.filesystem.FileIndexThread;

/**
 *
 * @author Gabriel
 */
public class SyncFiles {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        
       
        Collection<File> all = new ArrayList<>();
        File file = new File("C:\\Users\\Gabriel\\Documents\\TR22015FS\\hsqldb-2.3.2\\hsqldb\\"); 
        addTree(file, all);
 
        for (File temp : all) {
            FileIndexThread indexer = new FileIndexThread(temp);
            indexer.start();
        }
        //System.out.println(all);
        
        if (DBConnectionManager.createConnection())
        {
            Connection c = DBConnectionManager.getConnection();
        }
    }
    
    static void addTree(File file, Collection<File> all) {
        File[] children = file.listFiles();
        if (children != null) {
            for (File child : children) {
                all.add(child);
                addTree(child, all);
            }
        }
    }
}
