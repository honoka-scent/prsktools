'use client';

import React from 'react';
import { Grid, Card, CardContent, Container, Typography, Box, FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import { DefaultizedPieValueType } from '@mui/x-charts/models';
import { PieChart, pieArcLabelClasses } from '@mui/x-charts/PieChart';
import { ProcessedEntry, Song } from '../types/data';

// カラーの定義
interface ChartProps {
    entries: ProcessedEntry[];
    songs: Song[];
}

// const COLORS = ['#0088FE', '#00C49F', '#FFBB28'];

const LevelPieChart: React.FC<ChartProps> = ({ entries, songs }) => {
    const [filterDifficulty, setFilterDifficulty] = React.useState<string>('All');
    const uniqueDifficulties = React.useMemo(() => {
        const difficulties = entries.map((entry) => entry.difficulty).filter((diff) => diff !== null);
        return Array.from(new Set(difficulties)) as string[];
    }, [entries]);

    return (
        <Container>
            <Box mb={2} display="flex" flexDirection="column" gap={2} p={2}>
                {/* フィルターのドロップダウン */}
                <Box display="flex" gap={2}>
                    {/* 難易度フィルター */}
                    <FormControl variant="outlined" style={{ minWidth: 150 }}>
                        <InputLabel id="difficulty-label">難易度</InputLabel>
                        <Select
                            labelId="difficulty-label"
                            label="難易度"
                            value={filterDifficulty}
                            onChange={(e) => setFilterDifficulty(e.target.value)}
                        >
                            <MenuItem value="All">全て</MenuItem>
                            {uniqueDifficulties.map((diff) => (
                                <MenuItem key={diff} value={diff}>
                                    {diff}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                </Box>
            </Box>

            <Grid container spacing={2}>
                {/* 検索ボックスとフィルターの追加 */}
                {
                    songs.map((item) => {
                        // 各項目の値を取得し、undefined を 0 に置き換える
                        let songCount: number = 0;
                        if (filterDifficulty === 'Expert') {
                            songCount = (item.Expert ?? 0);
                        };
                        if (filterDifficulty === 'Master') {
                            songCount = (item.Master ?? 0);
                        };
                        if (filterDifficulty === 'Append') {
                            songCount = (item.Append ?? 0);
                        };
                        if (filterDifficulty === 'All') {
                            songCount = (item.Expert ?? 0) + (item.Master ?? 0) + (item.Append ?? 0);
                        };
                        const filteredEntry = entries.filter((entry) => entry.level === item.level && (filterDifficulty === 'All' || entry.difficulty === filterDifficulty));
                        if (songCount === 0) return null;
                        const fcCount = filteredEntry.filter((entry) => entry.level === item.level && entry.status === 'FC').length;
                        const apCount = filteredEntry.filter((entry) => entry.level === item.level && entry.status === 'AP').length;
                        const chartData = [
                        ];
                        if (apCount !== 0) {
                            chartData.push({ label: 'AP', value: apCount, color: '#f16ba6' });
                        }
                        if (fcCount !== 0) {
                            chartData.push({ label: 'FC', value: fcCount, color: '#7ec8ef' });
                        }
                        chartData.push({ label: 'None', value: (songCount - fcCount - apCount), color: '#d2b48c' });

                        // 全ての値が0の場合は表示しない
                        const total = chartData.reduce((acc, curr) => acc + curr.value, 0);
                        if (total === 0) return null;

                        const getArcLabel = (params: DefaultizedPieValueType) => {
                            const percent = params.value / songCount;
                            return `${(percent * 100).toFixed(0)}%`;
                        };

                        return (
                            <Grid item xs={12} sm={6} md={4} lg={3} key={item.level}>
                                <Card>
                                    <CardContent>
                                        <Typography variant="h6" align="center" gutterBottom>
                                            Level {item.level} ({songCount})
                                        </Typography>
                                        <PieChart
                                            series={[{
                                                data: chartData,
                                                arcLabel: getArcLabel,
                                            }]}
                                            sx={{
                                                [`& .${pieArcLabelClasses.root}`]: {
                                                    fill: 'white',
                                                    fontSize: 14,
                                                },
                                            }}
                                            slotProps={{
                                                legend: {
                                                    direction: "column",
                                                    position: {
                                                        vertical: 'middle',
                                                        horizontal: 'right',
                                                    },
                                                    itemMarkWidth: 20,
                                                    itemMarkHeight: 20,
                                                    markGap: 5,
                                                    itemGap: 10,
                                                }
                                            }}
                                            width={272}
                                            height={240}
                                        // colors={COLORS}
                                        >
                                        </PieChart>
                                    </CardContent>
                                </Card>
                            </Grid>
                        );
                    })}
            </Grid>
        </Container >
    );
};

export default LevelPieChart;