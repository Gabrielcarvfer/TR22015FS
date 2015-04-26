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
public class FileIndexThread extends Thread
{
    private Path path;
    public FileIndexThread (File file){
        this.path = file.toPath();
    }
    @Override
    public void run()
    {
        System.out.println("FileIndexThread running\n");
        BasicFileAttributes attr;
        
        try {
            attr = Files.readAttributes(this.path, BasicFileAttributes.class);
            System.out.println("fileName: " + path.getFileName());
            System.out.println("creationTime: " + attr.creationTime());
            System.out.println("lastAccessTime: " + attr.lastAccessTime());
            System.out.println("lastModifiedTime: " + attr.lastModifiedTime());
            System.out.println("isDirectory: " + attr.isDirectory());
            System.out.println("isOther: " + attr.isOther());
            System.out.println("isRegularFile: " + attr.isRegularFile());
            System.out.println("isSymbolicLink: " + attr.isSymbolicLink());
            System.out.println("size: " + attr.size());
            
        } catch (IOException ex) {
            Logger.getLogger(FileIndexThread.class.getName()).log(Level.SEVERE, null, ex);
        }

        
    }
}
