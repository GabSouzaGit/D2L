function createBlock(){
    const block = document.createElement("div");
    block.classList.add("block")

    const removeButton = document.createElement("div");

    removeButton.classList.add("remove-block");
    removeButton.textContent = "Remover"
    
    function remover(evt){
        removeButton.removeEventListener('click', remover)

        block.remove();
    }

    removeButton.addEventListener('click', remover)
    block.appendChild(removeButton)

    return block
}

export default function addBlock(){
    const block = createBlock()

    BLOCKS_CONTAINER.prepend(block)
}