# Ithaca setup — local Windows development

1. Stop the existing Flask app with **Ctrl+C**.
2. Back up your existing `ithaca` folder.
3. Copy the updated files into that folder. Choose **Replace files** and keep `.venv` and `.env`.
4. Install dependencies:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

5. Go to https://www.mongodb.com/cloud/atlas/register, create a free cluster, a database user, and allow your **current IP** under **Network Access**.
6. Under your cluster's **Connect → Drivers → Python**, copy the connection string. Add these lines to your existing `.env` (do not delete your Gemini key):

   ```dotenv
   MONGODB_URI=mongodb+srv://USER:PASSWORD@YOUR_CLUSTER.mongodb.net/?retryWrites=true&w=majority
   MONGODB_DB=ithaca
   ```

7. Test connection:

   ```powershell
   .\.venv\Scripts\python.exe database_status.py
   ```

8. Run the application:

   ```powershell
   .\.venv\Scripts\python.exe app.py
   ```

9. Open http://127.0.0.1:5000/journey and confirm the status says **Saved in browser and MongoDB Atlas**. Your earlier 75 XP and saved assessments should still be visible.
10. Complete a new quest or practice set, then open Atlas Data Explorer / Browse Collections, database `ithaca`, collections `profiles` and `progress`.

**Never share screenshots showing your MongoDB URI, database password, or Gemini API key.** Keep `.env` private and excluded from Git. The application remains a local demonstration, not a production student account system.
