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

/**
 *
 * @author Gabriel
 */
public class FolderRepairThread {
    private Path path;
    private File file;
    
    public FolderRepairThread (File file){
        this.path = file.toPath();
        this.file = file;
        
    }
    public synchronized void run()
    {
        
        //System.out.println("FileIndexThread running\n");
        BasicFileAttributes attr = null;
        
        try {
            attr = Files.readAttributes(this.path, BasicFileAttributes.class);
        } catch (IOException ex) {
            Logger.getLogger(FileIndexThread.class.getName()).log(Level.SEVERE, null, ex);
        }
        
        if (attr != null && attr.isDirectory() == true)
        {
            this.file.mkdirs();
        }
    }
}
