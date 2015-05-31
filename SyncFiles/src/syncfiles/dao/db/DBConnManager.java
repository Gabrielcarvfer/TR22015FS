/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package syncfiles.dao.db;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author Gabriel
 */
public class DBConnManager 
{
    private static final String DB_URL = "jdbc:sqlite:sync.db";
    private static Connection conn = null;
    private static Statement stmt = null;
    private static boolean driverInitialized;
    
    public static boolean initializeDatabaseConnection()
    {
       return loadDriver(DB_URL);
    }
    
    public static boolean initializeDatabaseConnection(String serverAddress)
    {
        return loadDriver(serverAddress);
    }
    
    public synchronized static ResultSet runQueryAndReturn(String sql)
    {       
        try 
        {
            loadDriver(DB_URL);
            ResultSet rs;
            rs = stmt.executeQuery(sql);
            return rs;
        } 
        catch (SQLException ex) 
        {
            Logger.getLogger(DBConnManager.class.getName()).log(Level.SEVERE, null, ex);
        }
        return null;
    }
    
    public synchronized static void runQuery(String sql)
    {
        try
        {
            loadDriver(DB_URL);
            stmt.execute(sql);
        }catch (SQLException ex)
        {
            Logger.getLogger(DBConnManager.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
    
    public synchronized static boolean closeDatabaseConnection(){   
        try {
            stmt.close();
            conn.close();
            driverInitialized = false;
            return true;
        } catch (SQLException ex) {
            Logger.getLogger(DBConnManager.class.getName()).log(Level.SEVERE, null, ex);
            return false;
        }
    }
    
    private synchronized static boolean loadDriver (String dbUrl)
    {
        if (driverInitialized == true)
        {
            return true;
        }
        else
        {
            try {
                Class.forName("org.sqlite.JDBC");
                conn = DriverManager.getConnection(dbUrl);
                stmt = conn.createStatement();
                driverInitialized = true;
                return true;
            } catch (ClassNotFoundException | SQLException ex) {
                Logger.getLogger(DBConnManager.class.getName()).log(Level.SEVERE, null, ex);
                return false;
            }
        }
    }
}
