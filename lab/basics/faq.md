### **Q: Firewall Issue – I cannot access services on ports. How can I troubleshoot this?**

**A:** If you’re unable to access services on specific ports due to firewall or network restrictions, you can use an SSH tunnel to securely forward the remote service to your local machine. For example, to access a service running on port `8443` on a remote server (`34.58.57.156`), follow these steps using PuTTY:

1. **Open PuTTY**.
2. In the **Session** tab:

   * Set **Host Name** to `PROVIDED_IP_ADDRESS`
   * Set **Port** to `22` (unless SSH runs on a different port)
   * Ensure **Connection type** is `SSH`
3. In the sidebar, go to **Connection → SSH → Tunnels**.
4. In the **Add new forwarded port** section:

   * **Source port:** `8443` (local port)
   * **Destination:** `localhost:8443` (remote address and port)
   * Click **Add** (you'll see `L8443  localhost:8443` added)
5. Return to the **Session** tab and click **Open**.
6. Log in using your SSH credentials.

Once connected, navigate to `https://localhost:8443` in your browser to access the remote service locally.

