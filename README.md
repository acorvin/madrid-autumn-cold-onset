# The First Cold Night, Madrid 1920–2025

When the first night below 5°C arrives each autumn at Madrid's Retiro weather station, and whether it still comes when it used to. The analysis is in [`notebooks/analysis.ipynb`](notebooks/analysis.ipynb).

## The problem

Every autumn in Madrid there is a first night when the temperature drops below 5°C. I wanted to know whether that night now comes later than it did a century ago, and how much of any change comes from the city around the station rather than the wider climate.

## What I did

I took NOAA's daily minimum temperatures for Madrid Retiro from 1920 and found the first night below 5°C in each autumn, counting from August 1. I kept an autumn only when no night was missing before its first cold night, which left 100 of 106. I compared the first thirty years with the last thirty, fitted a trend, and tested how much the result depends on the gaps in the record and on the 5°C line. To separate the city from the climate, I ran the same calculation on ERA5, a reanalysis of the wider area. For this autumn I used AEMET's own daily record for the station, because NOAA's newest values are hourly lows. The notebook ends by recomputing the main figures with plain Python and stops if any of them differ.

## What it found

- The first cold night moved from October 23 on average (1920 to 1949) to November 6 (1996 to 2025), about two weeks later.
- In 25 of the 28 early autumns a night below 5°C had come by the end of October. In the recent period it was 8 of 26.
- The three latest first cold nights in the record all came after 1990, and the date moved later by about 1.8 days a decade.
- The average November went from 16.1 nights below 5°C to 10.0.
- The wider area moved later too, by 7.9 days against 10.0 at the station between 1940 to 1969 and 1996 to 2025.
- This autumn's first night below 5°C was November 4, at 4.7°C.

## Data

| Layer | Source | Notes |
|---|---|---|
| Station record, 1920–2026 | NOAA GHCN-Daily, station SP000003195 (Madrid Retiro) | Daily minimum temperature in tenths of a degree, with measurement, quality and source flags |
| Wider area, 1940–2026 | ERA5 through the Open-Meteo historical weather API | Daily minimum for the grid square around Retiro, about 25 kilometers across |
| This autumn | AEMET OpenData, station 3195 (Madrid, Retiro) | Official daily values from August 1, 2026 |

`scripts/download_data.py` downloads all three into `data/raw`. AEMET needs a free API key from https://opendata.aemet.es, set as `AEMET_API_KEY`.

## Method

- **Quality.** The 14 minimum temperatures that failed a GHCN quality check are dropped.
- **First cold night.** An autumn runs from August 1 to July 31, and its first cold night is the first night below 5°C. An autumn counts only if no night is missing before that date.
- **Periods.** 1920 to 1949 against 1996 to 2025, and for the ERA5 comparison 1940 to 1969 against 1996 to 2025, because ERA5 starts in 1940.
- **Trend.** Theil-Sen slope with its 95% interval, and Kendall's tau.
- **Gaps.** As a worst case, every incomplete autumn is put back at the earliest date its gap allows. The recent autumns still come out 9.6 days later.
- **The 5°C line.** At 3°C the shift is 18.8 days, and at 0°C it is 26.9 days.
- **This autumn.** From September 29, 2026, NOAA's minimums for the station carry measurement flag "H", the lowest hourly reading, which can miss the true overnight low. No earlier value carries it, so 1920 to 2025 is not affected, and this autumn comes from AEMET.

## Limitations

- This is one station in one city.
- ERA5's squares are coarse and include part of Madrid, so they narrow down the city's share without separating it cleanly. Its last few weeks are preliminary.
- The 5°C line is a choice. Other lines change the size of the shift but not its direction.
- NOAA adds data over time, so a fresh download can change the most recent years slightly.

## Run it

```
pip install -r requirements.txt
python3 scripts/download_data.py   # optional: the data in data/raw is from November 17, 2026
jupyter lab notebooks/analysis.ipynb
```

The notebook writes `data/processed/first_cold_night.csv`, `data/processed/november_cold_nights.csv` and the two charts in `charts/`.
