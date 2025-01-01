async function getConfig() {
    // Fetch the config file using the runtime URL
    const response = await fetch(chrome.runtime.getURL("config.json"));
    const config = await response.json();
    return config;
  }
  
  document.getElementById("send-album").addEventListener("click", async () => {
    // Load configuration
    const config = await getConfig();
    const apiUrl = config.API_URL;
    const secretToken = config.API_SECRET_TOKEN;
  
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const url = tab.url;
    const statusElement = document.getElementById("status");
  
    // Validate the URL
    const regex = /^https:\/\/www\.qobuz\.com\/[a-zA-Z\-]+\/album\/[a-zA-Z0-9\-]+\/[a-zA-Z0-9]+$/;
    if (!regex.test(url)) {
      statusElement.textContent = "Invalid URL. Please navigate to a valid Qobuz album page.";
      return;
    }
  
    // Send the URL to the API
    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${secretToken}`
        },
        body: JSON.stringify({ url })
      });
  
      if (response.ok) {
        statusElement.textContent = "Album sent successfully!";
      } else {
        const error = await response.json();
        statusElement.textContent = `Error: ${error.error}`;
      }
    } catch (error) {
      statusElement.textContent = `Error: ${error.message}`;
    }
  });
  