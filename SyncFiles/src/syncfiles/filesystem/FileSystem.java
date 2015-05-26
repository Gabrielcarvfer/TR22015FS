/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package syncfiles.filesystem;

import java.io.File;
import java.util.ArrayList;
import java.util.Collection;
import syncfiles.dao.DBConnManager;

/**
 *
 * @author Gabriel
 */
public class FileSystem {
    
    
    public boolean reIndexFolder(File folder)
{
        Collection<File> all = new ArrayList<>();
        addTree(folder, all);
 
        for (File temp : all) 
        {
            FileFolderIndexThread indexer = new FileFolderIndexThread(temp);
            indexer.start();
            
        }
        for (File temp : all)
        {
            FolderRepairThread repairer = new FolderRepairThread(temp);
            repairer.run();
        }
  
        DBConnManager.closeDatabaseConnection();
        return true;
}

private void addTree(File file, Collection<File> all) {
        File[] children = file.listFiles();
        if (children != null) {
            for (File child : children) {
                all.add(child);
                addTree(child, all);
            }
        }
    }
}


