package main

import (
	"bufio"
	"image/color"
	"log"
	"os"
	"strconv"
	"strings"

	"github.com/fogleman/gg"
)

func main() {
	file, err := os.Open("runs/2018-12-03 16 14.run")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)

	// Eat two lines
	scanner.Scan()
	scanner.Scan()

	width := 500
	height := 500

	maxTime := 500.0
	numEpisodes := 30000.0

	img := gg.NewContext(width, height)

	img.SetColor(color.RGBA{255, 255, 255, 255})
	for x := 0; x < width; x++ {
		for y := 0; y < height; y++ {
			img.SetPixel(x, y)
		}
	}

	img.SetColor(color.RGBA{0, 0, 0, 255})

	for scanner.Scan() {
		result := strings.Split(scanner.Text(), ", ")

		episodeParsed, _ := strconv.ParseFloat(result[0], 64)
		if err != nil {
			panic(err)
		}

		timeParsed, err := strconv.ParseFloat(result[1], 64)
		if err != nil {
			panic(err)
		}

		x := height - int((episodeParsed/numEpisodes)*float64(width))
		y := int((timeParsed / maxTime) * float64(height))

		img.SetPixel(x, y)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	err = img.SavePNG("runs/out.png")
	if err != nil {
		log.Fatal(err)
	}
}
