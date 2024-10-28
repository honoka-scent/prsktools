// frontend/components/DataTable.tsx

'use client';

import React, { useState, useMemo } from 'react';
import { DataGrid, GridColDef, GridLogicOperator } from '@mui/x-data-grid';
import { Container, Typography, TextField, Box, FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import { ProcessedEntry } from '../types/data';

interface DataTableProps {
    entries: ProcessedEntry[];
    // songInfos: Song[];
}

const columns: GridColDef[] = [
    { field: 'name', headerName: '曲名', width: 400 },
    { field: 'difficulty', headerName: '難易度', width: 150 },
    { field: 'level', headerName: 'レベル', width: 100 },
    { field: 'status', headerName: 'ステータス', width: 100 },
    { field: 'date', headerName: '達成日', width: 200 },
];

// const toggleFilter = () => {
// };

const initialFilterModel = {
    items: [
        // { columnField: 'name', operatorValue: 'contains', value: '' },
        // { columnField: 'difficulty', operatorValue: 'contains', value: '' },
        // { columnField: 'level', operatorValue: 'contains', value: '' },
        // { field: 'status', operator: 'contains', 'value': 'FC' },
        // { field: 'status', operator: 'contains', 'value': 'AP' },
        { field: 'status', operator: 'isNotEmpty' },
        // { columnField: 'date', operatorValue: 'isNotEmpty' },
    ],
    logicOperator: GridLogicOperator.And,
};

const DataTable: React.FC<DataTableProps> = ({ entries }) => {
    // フィルターの表示状態を管理する状態
    // const [showFilter, setShowFilter] = useState<boolean>(false);

    // 検索入力を管理する状態
    const [searchText, setSearchText] = useState<string>('');

    // 各フィルターの状態を管理する状態
    const [filterDifficulty, setFilterDifficulty] = useState<string>('All');
    const [filterLevel, setFilterLevel] = useState<string>('All');
    const [filterStatus, setFilterStatus] = useState<string>('All');

    // フィルターのトグル関数
    // const toggleFilter = () => {
    //     setShowFilter((prev) => !prev);
    // };

    // フィルタリングされたエントリを計算
    const filteredEntries: ProcessedEntry[] = useMemo(() => {
        return entries.filter((entry) => {
            // 曲名検索フィルター
            const matchesSearchText = entry.name.toLowerCase().includes(searchText.toLowerCase());

            // 難易度フィルター
            const matchesDifficulty = filterDifficulty === 'All' || entry.difficulty === filterDifficulty;

            // レベルフィルター
            const matchesLevel =
                filterLevel === 'All' ||
                (filterLevel === 'Unknown' && (entry.level === null || entry.level === 0)) ||
                (filterLevel !== 'Unknown' && entry.level === Number(filterLevel));

            // ステータスフィルター
            const matchesStatus = filterStatus === 'All' || entry.status === filterStatus;

            // すべての条件を満たす場合に含める
            return matchesSearchText && matchesDifficulty && matchesLevel && matchesStatus;
        });
    }, [entries, searchText, filterDifficulty, filterLevel, filterStatus]);

    // ユニークな難易度、レベル、ステータスのリストを作成
    const uniqueDifficulties = useMemo(() => {
        const difficulties = entries.map((entry) => entry.difficulty).filter((diff) => diff !== null);
        return Array.from(new Set(difficulties)) as string[];
    }, [entries]);

    const uniqueLevels = useMemo(() => {
        const levels = entries.map((entry) => entry.level).filter((lvl) => lvl !== null && lvl !== 0);
        const levelNumbers = Array.from(new Set(levels)) as number[];
        levelNumbers.sort((a, b) => a - b); // 昇順にソート
        return levelNumbers.map((lvl) => lvl.toString());
    }, [entries]);

    const uniqueStatuses = useMemo(() => {
        const statuses = entries.map((entry) => entry.status).filter((status) => status !== null);
        return Array.from(new Set(statuses)) as string[];
    }, [entries]);

    return (
        <Container style={{ marginTop: '2rem' }}>
            <Typography variant="h4" gutterBottom>
                アチーブメント一覧
            </Typography>
            {/* 検索ボックスとフィルターの追加 */}
            <Box mb={2} display="flex" flexDirection="column" gap={2}>
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

                    {/* レベルフィルター */}
                    <FormControl variant="outlined" style={{ minWidth: 150 }}>
                        <InputLabel id="level-label">レベル</InputLabel>
                        <Select
                            labelId="level-label"
                            label="レベル"
                            value={filterLevel}
                            onChange={(e) => setFilterLevel(e.target.value)}
                        >
                            <MenuItem value="All">全て</MenuItem>
                            <MenuItem value="Unknown">不明</MenuItem>
                            {uniqueLevels.map((lvl) => (
                                <MenuItem key={lvl} value={lvl}>
                                    {lvl}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>

                    {/* ステータスフィルター */}
                    <FormControl variant="outlined" style={{ minWidth: 150 }}>
                        <InputLabel id="status-label">ステータス</InputLabel>
                        <Select
                            labelId="status-label"
                            label="ステータス"
                            value={filterStatus}
                            onChange={(e) => setFilterStatus(e.target.value)}
                        >
                            <MenuItem value="All">全て</MenuItem>
                            {uniqueStatuses.map((status) => (
                                <MenuItem key={status} value={status}>
                                    {status}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                </Box>
                {/* 曲名検索ボックス */}
                <TextField
                    label="曲名検索"
                    variant="outlined"
                    fullWidth
                    value={searchText}
                    onChange={(e) => setSearchText(e.target.value)}
                />

            </Box>
            <div style={{ height: 600, width: '100%' }}>
                <DataGrid
                    rows={filteredEntries}
                    columns={columns}
                    // pageSize={10}
                    pageSizeOptions={[10, 20, 50]}
                    initialState={{
                        filter: { filterModel: initialFilterModel },
                        sorting: {
                            sortModel: [{ field: 'date', sort: 'desc' }],
                        },
                    }}
                    // components={{
                    //     // Toolbar: CustomToolbar,
                    // }}
                    // componentsProps={{
                    //     toolbar: {
                    //         showFilter: showFilter,
                    //         toggleFilter: toggleFilter,
                    //     },
                    // }}
                    disableRowSelectionOnClick
                    filterMode="client"
                // disableColumnFilter={!showFilter}
                />
            </div>
        </Container>
    );
};

export default DataTable;
