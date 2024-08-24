const mode = document.getElementById("mode")
const userText = document.getElementById("text")
const urlText = document.getElementById("url")
const fileText = document.getElementById("file")

const outputText = document.getElementById("summary")
const submitButton = document.getElementById("submit")

let curMode = 0

const containers = ["text-container", "url-container", "file-container"]
const shown =
  "display: flex; flex-direction: column; align-items: center; width: 100%;"
const hidden = "display: none;"

/* setInitialDisplay(containers, shown, hidden)

// Set initial display styles
function setInitialDisplay(containers, shown, hidden) {
  containers.forEach((id, index) => {
    document.getElementById(id).style.cssText = index === 0 ? shown : hidden
  })
} */

// Change the display of the containers
function changeContainerDisplay(nextIndex, containers, shown, hidden) {
  containers.forEach((id, index) => {
    document.getElementById(id).style.cssText =
      index === nextIndex ? shown : hidden
  })
}

async function getPdfContent(file) {
  const fileReader = new FileReader()

  return new Promise((resolve, reject) => {
    fileReader.onload = async (event) => {
      const typedArray = new Uint8Array(event.target.result)

      try {
        const pdf = await pdfjsLib.getDocument(typedArray).promise
        let pdfContent = ""

        for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
          const page = await pdf.getPage(pageNum)
          const text = await page.getTextContent()

          pdfContent += text.items.map((item) => item.str).join(" ")
        }

        resolve(pdfContent)
      } catch (error) {
        reject(error)
      }
    }

    fileReader.onerror = (error) => reject(error)

    fileReader.readAsArrayBuffer(file)
  })
}

async function getData(curMode) {
  if (curMode === 0) {
    if (userText.value === "") {
      alert("Please enter some text")
      return
    }
    return userText.value
  } else if (curMode === 1) {
    if (urlText.value === "") {
      alert("Please enter a url")
      return
    }
    // check if url is valid
    try {
      new URL(urlText.value)
    } catch (error) {
      alert("Please enter a valid url")
      return
    }

    return urlText.value
  } else if (curMode === 2) {
    // check if pdf or text file
    if (fileText.files[0]) {
      const file = fileText.files[0]
      if (file.type === "application/pdf") {
        return await getPdfContent(file)
      } else {
        alert("Please upload a pdf file")
        return // if not pdf
      }
    }
  } else {
    alert("Something went wrong")
    return
  }
}

// Cycle through the modes
mode.addEventListener("click", function () {
  const modes = ["TEXT", "URL", "FILE"]
  let currentMode = mode.innerHTML

  let index = modes.indexOf(currentMode) || 0
  let nextIndex = (index + 1) % modes.length
  curMode = nextIndex

  console.log(curMode)

  mode.innerHTML = modes[nextIndex]

  changeContainerDisplay(nextIndex, containers, shown, hidden)
})

// Submit the text to the server
submitButton.addEventListener("click", async function () {
  const text = await getData(curMode)

  console.log(text)
  console.log(text.length)
  /* axios  
      .post("http://127.0.0.1:8000/summary", {
        mode: curMode,
        text: text,
        url: url,
        sum_len: "long",
      })
      .then(function (response) {
        outputText.innerHTML = response.data
      })
      .catch(function (error) {
        console.log(error)
      }) */
})
