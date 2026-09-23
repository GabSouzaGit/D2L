import addBlock from "./javascript/blockLogic.js";

const blockAdder = document.querySelector("#add-block-button");

blockAdder.addEventListener("click", () => {
    addBlock()
})