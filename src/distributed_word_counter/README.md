Module 3 **without concurrency** was merged to master. It contains select multiplexed server.

Module 3 **with concurrency** is at branch third-module-concurrent and **is not merged to master**

    Tutorial:
    
    To use the application, save the text files you want to analyse
    into the server/files directory.
    
    You need also to have mongodb into your machine, because it's
    the database used to store the files on server side.
    
    Then, run the DatabaseHandler class as main, so that the files are
    loaded into mongodb collection.
    
    Run serverMain and clientMain to start communication. You can pass
    the port to use as args[0] for both.
    
    You can run as many clients as you want, just change the
    numToListen attribute on ServerConnector.py .