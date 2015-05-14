/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package syncfiles.filesystem;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.logging.Level;
import java.util.logging.Logger;
import syncfiles.dao.DAOFiles;

/**
 *
 * @author Gabriel
 */
public class FileFolderIndexThread extends Thread
{
    private Path path;
    
    public FileFolderIndexThread (File file){
        this.path = file.toPath();
        
    }
    @Override
    public synchronized void run()
    {
        
        //System.out.println("FileIndexThread running\n");
        BasicFileAttributes attr = null;
        
        try {
            attr = Files.readAttributes(this.path, BasicFileAttributes.class);
        } catch (IOException ex) {
            Logger.getLogger(FileFolderIndexThread.class.getName()).log(Level.SEVERE, null, ex);
        }
        
        if (attr != null)
        {
            System.out.println("Including file:\n");
            DAOFiles.insertNewFile (path.getFileName().toString(), attr.size(), attr.creationTime().toString(),
                    attr.lastModifiedTime().toString(), path.toString(), attr.isDirectory() );  
            System.out.println("Removing file:\n");
            DAOFiles.removeFile(path.toString());
        }
    }
}
