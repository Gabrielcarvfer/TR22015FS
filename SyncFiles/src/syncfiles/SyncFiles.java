/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package syncfiles;

import java.io.File;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.Collection;
import syncfiles.dao.DBConnManager;
import syncfiles.filesystem.FileFolderIndexThread;

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
    public static void main(String[] args) throws InterruptedException, UnknownHostException {
        
        DBConnManager.initializeDatabaseConnection();
        
       //Cria árvore que percorre arquivos e pastas
        Collection<File> all = new ArrayList<>();
        File file = new File("C:/Users/Gabriel/Documents/TR22015FS/SyncFiles/"); 
        addTree(file, all);
 
        for (File temp : all) {
            FileFolderIndexThread indexer = new FileFolderIndexThread(temp);
            int i = 100000;
            while(i> 0)
            {
                i--;
            }
            indexer.start();
            
        }
        
        
       if(DBConnManager.closeDatabaseConnection())
        {
            //yay
        }
        else
        {
            //shooo
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
