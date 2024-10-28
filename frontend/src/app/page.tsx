// frontend/app/page.tsx

import React from 'react';
// import { Card } from '@mui/material';
import DataTable from '../components/DataTable';
import PieChart from '../components/Chart';
import { DataJson, ProcessedEntry, Song, SongData } from '../types/data';
import path from 'path';
import fs from 'fs/promises';
import { mapDataToProcessedEntries, mapSongInfo } from '../utils/dataMapper';

const HomePage: React.FC = async () => {
  try {
    // 'archievements.json'のパスを取得
    const filePath = path.join(process.cwd(), 'public', 'achievements.json');
    const songFilePath = path.join(process.cwd(), 'public', 'song_info.json');

    // 'archievements.json'を読み込む
    const jsonData = await fs.readFile(filePath, 'utf-8');
    const songJsonData = await fs.readFile(songFilePath, 'utf-8');

    const data: DataJson = JSON.parse(jsonData);
    const songData: SongData = JSON.parse(songJsonData);

    // マッピング関数を使用してProcessedEntryの配列を取得
    const entries: ProcessedEntry[] = mapDataToProcessedEntries(data);
    const songInfos: Song[] = mapSongInfo(songData);
    console.log(songInfos);

    return <div>
      <DataTable entries={entries} />
      <PieChart entries={entries} songs={songInfos} />
    </div>;

  } catch (error) {
    console.error('Error reading or processing archievements.json:', error);
    return (
      <div>
        <h1>データの読み込みに失敗しました。</h1>
      </div>
    );
  }

};

export default HomePage;
