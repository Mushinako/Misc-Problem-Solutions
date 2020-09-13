function f(str: string, key: number) {
    const ptext = str.toUpperCase();
    const mainArray: string[][] = Array(key);
    for (let i = 0; i < key; i++) {
        mainArray[i] = Array(ptext.length);
        for (let s = 0; s < ptext.length; s++) {
            mainArray[i][s] = "";
        }
    }
    let j = 0;
    let r = 0;
    for (let i = 0; i < ptext.length; i++) {
        const p = ptext.substr(i, 1);
        mainArray[j][i] = p;
        if (r === 0) {
            j++;
        } else {
            j--;
        }
        if (j === key - 1) {
            r = 1;
        } else if (j === 0) {
            r = 0;
        }
    }
    const newMainArray: string[] = Array(key);
    for (let i = 0; i < mainArray.length; i++) {
        newMainArray[i] = mainArray[i].join("");
    }
    const ctext = newMainArray.join("");
    return ctext;
}

console.log(f("Hello,World!", 3));
console.log(f("Moby-Dick; or, The Whale is an 1851 novel by American writer Herman Melville. The book is the sailor Ishmael's narrative of the obsessive quest of Ahab, captain of the whaling ship Pequod, for revenge on Moby Dick, the giant white sperm whale that on the ship's previous voyage bit off Ahab's leg at the knee. Wikipedia", 10));