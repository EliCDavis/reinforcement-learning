package main

import (
	"bufio"
	"fmt"
	"image/color"
	"io/ioutil"
	"log"
	"os"
	"regexp"
	"strconv"
	"strings"

	"github.com/fogleman/gg"
)

func trimLeftChars(s string, n int) string {
	m := 0
	for i := range s {
		if m >= n {
			return s[i:]
		}
		m++
	}
	return s[:0]
}

func dot_plot(fileName string) {
	file, err := os.Open(fileName)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)

	// Eat two lines
	scanner.Scan()
	scanner.Scan()

	width := 1500
	height := 1000

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

		x := int((episodeParsed / numEpisodes) * float64(width))
		y := height - int((timeParsed/maxTime)*float64(height))

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

func processFile(folderName string, algorithm string, environment string, discritized int, discount float64) (int, float64) {
	fileRegex := fmt.Sprintf("%s- %s - %d - 0\\.%s2018.*.run", algorithm, environment, discritized, trimLeftChars(strconv.FormatFloat(discount, 'f', -1, 64), 2))

	files, err := ioutil.ReadDir(folderName)
	if err != nil {
		log.Fatal(err)
	}

	var fileName string
	for _, f := range files {
		matched, err := regexp.MatchString(fileRegex, f.Name())
		if err != nil {
			panic(err)
		}
		if matched {
			fileName = f.Name()
		}
	}

	if fileName == "" {
		panic("couldn't find file")
	}

	file, err := os.Open(fmt.Sprintf("%s/%s", folderName, fileName))
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)

	// Eat two lines
	scanner.Scan()
	scanner.Scan()

	var numOfEpisodesCompleted int
	var totalTimeToComplete int

	for scanner.Scan() {
		result := strings.Split(scanner.Text(), ", ")
		numOfEpisodesCompleted++

		timeParsed, err := strconv.Atoi(result[1])
		if err != nil {
			panic(err)
		}
		totalTimeToComplete += timeParsed

	}

	return numOfEpisodesCompleted, float64(totalTimeToComplete) / float64(numOfEpisodesCompleted)

}

func accumulationPlot(folderName string) {

	csv, _ := os.Create("acc.csv")
	w := bufio.NewWriter(csv)
	w.WriteString("environment, algorithm, dicritization, discount, solved, average time\n")
	algorithms := []string{"q", "sarsa"}
	envs := []string{"Acrobot-v1", "CartPole-v1", "MountainCar-v0"}
	discretizations := []int{0, 1, 2}
	discounts := []float64{.01, .05, .1, .2, .3, .4, .5, .6, .7, .8, .9, .95, .99}
	for _, environment := range envs {
		for _, discritized := range discretizations {
			for _, discount := range discounts {
				for _, algorithm := range algorithms {
					numE, avgTime := processFile(folderName, algorithm, environment, discritized, discount)
					w.WriteString(fmt.Sprintf("%s, %s, %d, %s, %d, %f\n", environment, algorithm, discritized, strconv.FormatFloat(discount, 'f', -1, 64), numE, avgTime))
				}
			}
		}
	}

}

func main() {
	accumulationPlot("fat")
}
