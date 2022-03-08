using UnityEngine;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

public class Client : MonoBehaviour
{
    static Socket server;

    void Start()
    {
        Connect("192.168.1.21", 8000);
    }

    void OnApplicationQuit()
    {
        byte[] buffer = new byte[1024];
        string msg = "!DISCONNECT";
        buffer = Encoding.ASCII.GetBytes(msg);
        server.Send(buffer);
    }

    public static void Connect(string host, int port)
    {
        byte[] buffer = new byte[1024];
        server = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

        Debug.Log("Establishing Connection to " + host);
        try
        {
            server.Connect("192.168.1.21", port);
            Debug.Log("Connection established");
            RecieveData(server, buffer);
            SendData(server, buffer);
        }
        catch
        {
            Debug.Log("Can't connected to server.");
        }
    }

    public static void RecieveData(Socket server, byte[] buffer)
    {
        //To recieving data from server
        int received = 0;
        received += server.Receive(buffer, 0 + received, buffer.Length - received, SocketFlags.None);
        string str = Encoding.UTF8.GetString(buffer, 0, buffer.Length);
        Debug.Log(str);
    }

    public static void SendData(Socket server, byte[] buffer)
    {
        //To send data to server
        string msg = "Hello server";
        buffer = Encoding.ASCII.GetBytes(msg);

        server.Send(buffer);
    }
}