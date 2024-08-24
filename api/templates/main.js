const inputMode = document.getElementById("mode")
const lengthMode = document.getElementById("length")
const userText = document.getElementById("text")
const urlText = document.getElementById("url")
const fileText = document.getElementById("file")
const outputText = document.getElementById("summary")
const submitButton = document.getElementById("submit")

// CSS Display Styles
const containers = ["text-container", "url-container", "file-container"]
const shown =
  "display: flex; flex-direction: column; align-items: center; width: 100%;"
const hidden = "display: none;"

// Initialize current mode to 'Text'
let curTextMode = 0

// Summary Length Mode
let curLengthMode = 0

// Initialize display styles based on the mode
setInitialDisplay(containers, shown, hidden)

/**
 * Sets the initial display styles for the input containers based on the current mode.
 * @param {Array} containers - Array of container element IDs.
 * @param {String} shown - CSS style for visible container.
 * @param {String} hidden - CSS style for hidden container.
 */
function setInitialDisplay(containers, shown, hidden) {
  containers.forEach((id, index) => {
    document.getElementById(id).style.cssText = index === 0 ? shown : hidden
  })
}

/**
 * Changes the display of containers when the mode is switched.
 * @param {Number} nextIndex - Index of the next container to be shown.
 * @param {Array} containers - Array of container element IDs.
 * @param {String} shown - CSS style for visible container.
 * @param {String} hidden - CSS style for hidden container.
 */
function changeContainerDisplay(nextIndex, containers, shown, hidden) {
  containers.forEach((id, index) => {
    document.getElementById(id).style.cssText =
      index === nextIndex ? shown : hidden
  })
}

/**
 * Reads the content of a PDF file and returns the extracted text.
 * @param {File} file - The PDF file to read.
 * @returns {Promise<String>} The text content extracted from the PDF.
 */
async function getPdfContent(file) {
  const fileReader = new FileReader()

  // Read the file as an array buffer
  const arrayBuffer = await new Promise((resolve, reject) => {
    fileReader.onload = () => {
      resolve(fileReader.result)
    }
    fileReader.onerror = reject
    fileReader.readAsArrayBuffer(file)
  })

  // Convert ArrayBuffer to Uint8Array
  const typedArray = new Uint8Array(arrayBuffer)

  try {
    // Get the PDF document
    const pdf = await pdfjsLib.getDocument(typedArray).promise
    let pdfContent = ""

    // Extract text from each page of the PDF
    for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
      const page = await pdf.getPage(pageNum)
      const content = await page.getTextContent()
      pdfContent += content.items.map((item) => item.str).join(" ")
    }

    return pdfContent
  } catch (error) {
    console.error(error)
    throw new Error("Error reading PDF file")
  }
}

/**
 * Validates user input based on the current mode and returns the input if valid.
 * @param {Number} curTextMode - The current mode of input (0: Text, 1: URL, 2: File).
 * @returns {Promise<String|null>} The validated input text, URL, or PDF content.
 */
async function getData(curTextMode) {
  if (curTextMode === 0) {
    if (userText.value === "") {
      alert("No Text Entered")
      return null
    }
    return userText.value
  } else if (curTextMode === 1) {
    if (urlText.value === "") {
      alert("No URL Entered")
      return null
    }

    try {
      new URL(urlText.value) // Validate URL format
    } catch (error) {
      alert("Invalid URL")
      return null
    }

    return urlText.value
  } else if (curTextMode === 2) {
    const file = fileText.files[0]
    if (file) {
      if (file.type === "application/pdf") {
        return await getPdfContent(file)
      } else {
        alert("No File Uploaded or Invalid File Type")
        return null
      }
    }
  } else {
    alert("Something went wrong")
    return null
  }
}

/**
 * Sends a POST request to the server to get a summary of the provided text or URL.
 * @param {Object} requestText - The text, URL, and mode to send in the request.
 * @returns {Promise<Object|null>} The summary response from the server, or null if an error occurred.
 */
async function getSummary(requestText) {
  try {
    const res = await axios.post("http://127.0.0.1:8000/summary", requestText, {
      headers: {
        "Content-Type": "application/json",
      },
    })

    if (res.status === 200 && res.data) {
      return res.data
    } else if (res.status === 422) {
      alert("Summarization failed: Unable to process the text.")
      return null
    } else if (res.status === 500) {
      alert("Internal Server Error: Please try again later.")
      return null
    } else if (res.status === 400) {
      alert("Bad Request: Invalid input or mode.")
      return null
    }

    alert("Unknown Error: Please try again later.")
    return
  } catch (error) {
    console.error("Error summarizing text:", error)
    alert("Network Error or Server is unreachable.")
    return null
  }
}

// Event listener to switch between text, URL, and file input modes
inputMode.addEventListener("click", function () {
  const modes = ["TEXT", "URL", "FILE"]
  let currentMode = inputMode.innerHTML

  let index = modes.indexOf(currentMode) || 0
  let nextIndex = (index + 1) % modes.length
  curTextMode = nextIndex

  inputMode.innerHTML = modes[nextIndex]

  changeContainerDisplay(nextIndex, containers, shown, hidden)
})

// Event listener to switch between summary length modes
lengthMode.addEventListener("click", function () {
  const lengths = ["SHORT", "MEDIUM", "LONG"]
  let currentLength = lengthMode.innerHTML

  let index = lengths.indexOf(currentLength) || 0
  let nextIndex = (index + 1) % lengths.length
  curLengthMode = nextIndex

  lengthMode.innerHTML = lengths[nextIndex]
})

// Event listener to submit the input to the server for summarization
submitButton.addEventListener("click", async function () {
  const resultText = await getData(curTextMode)

  if (!resultText) {
    console.error("No text to summarize")
    return
  }

  // Validate text length before sending to the server
  if (resultText.length > 2000) {
    alert("Content too long (max 2000 characters)")
    return
  }

  let requestText = {
    text: "",
    url: "",
    mode: curTextMode,
    sumlen: curLengthMode,
  }

  if (curTextMode === 0 || curTextMode === 2) {
    requestText.text = resultText
  } else if (curTextMode === 1) {
    requestText.url = resultText
  }

  // Display loading message while awaiting summary
  outputText.innerHTML = "Loading..."

  const summary = await getSummary(requestText)

  // Display the summary or clear if no summary returned
  if (summary) {
    outputText.innerHTML = summary.summary
  } else {
    outputText.innerHTML = ""
  }
})
