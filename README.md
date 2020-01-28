# UK Energy Viewer

This is a project I started after submitting my PhD to build tools that can be used to access and graph the UK's energy mix. It is intended to be a learning exercise for me, but if you find anything useful then feel free to use it.


The data comes from the [Elexon portal](https://www.elexonportal.co.uk/scripting). To access their data you need to create a free account and then make a file called 'API_Key.txt' to store your API key in. I've also used a file called 'LastAccessed.txt', which stores the last time the live data was accessed in the form YYYY-MM-DD hh:mm:ss and does not allow reaccess of the data within five minutes.

I used some of the details [here](https://energyanalyst.co.uk/uk-power-market-data-python-xml-and-pandas-dataframes/) to get started, although they have quite a different approach.

## Author

**Peter Griffin**

## License
This software is released under an MIT License

Copyright (c) 2019 Peter Griffin

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. 

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
