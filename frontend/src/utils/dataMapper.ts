// frontend/utils/dataMapper.ts

import { DataJson, ResultEntry, ProcessedEntry, ResultCategory, Song, SongData } from '../types/data';

/**
 * ResultEntryからProcessedEntryへのマッピング関数
 * @param data DataJson形式のデータ
 * @returns ProcessedEntryの配列
 */
export const mapDataToProcessedEntries = (data: DataJson): ProcessedEntry[] => {
    const entries: ProcessedEntry[] = [];
    let idCounter = 0;

    Object.values(data.results).forEach((item: ResultEntry) => {
        ['Expert', 'Master', 'Append'].forEach((difficulty) => {
            const category = item[difficulty as keyof Omit<ResultEntry, 'name' | 'date'>] as ResultCategory;

            // levelを数値に変換、変換できない場合はnull
            const level = category.level && category.level !== '-' ? Number(category.level) : 0;

            entries.push({
                id: idCounter++,
                name: item.name,
                difficulty: difficulty as 'Expert' | 'Master' | 'Append',
                level: isNaN(level) ? null : level,
                status: category.status || null,
                date: category.date ? new Date(category.date).toLocaleString() : null,
            });
        });
    });

    return entries;
};

/**
 * JSONデータをMappedData形式に変換する関数
 * @param data - 元のJSONデータ
 * @returns MappedData形式のデータ
 */
export const mapSongInfo = (data: SongData): Song[] => {
    // song_count を配列に変換
    const songs: Song[] = Object.entries(data.song_count).map(([key, counts]) => ({
        level: parseInt(key, 10),
        Expert: counts.Expert,
        Master: counts.Master,
        Append: counts.Append,
    }));

    return songs;
    // return {
    //     songs,
    //     diffCount: data.diff_count,
    // };
};