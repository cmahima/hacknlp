export {
    getGradientColors,
    getColor
}

function getGradientColors(percentageValue) {
    let per = parseInt(percentageValue * 100, 10);
    per = per > 10 ? per - 10 : per;
    let colors = [];
    for (let i = 0; (i < 7 && per < 100); i++) {
        const value = per / 100;
        const color = getColor(value);
        colors.push(color)
        per = per + 5;
        per = per > 100 ? 100 : per;
    }
    return colors.join(",");
}

//~--- Helper functions

function getColor(value) {
    const hue = ((1 - value) * 120).toString(10);
    // return ["hsl(", hue, ",100%,50%)"].join("");
    return ["hsl(", hue, ",80%,50%)"].join("");
}