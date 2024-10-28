// export interface Category {
//     level: number | null;
//     difficulty: string | null;
//     status: string | null;
//     date: string | null;
// }

export interface ResultCategory {
    status: string | null;
    date: string | null;
    level: string | null;
}

export interface ResultEntry {
    name: string;
    Expert: ResultCategory;
    Master: ResultCategory;
    Append: ResultCategory;
    date: string | null;
}

export interface DataJson {
    results: {
        [key: string]: ResultEntry;
    }
}

export interface ProcessedEntry {
    id: number;
    name: string;
    difficulty: string | null;
    level: number | null;
    status: string | null;
    date: string | null;
}

// 各楽曲の難易度ごとのカウント
export interface DifficultyCounts {
    Expert?: number;
    Master?: number;
    Append?: number;
}

// song_count の各エントリ
interface SongCountEntry {
    level: number;
    Difficulties: DifficultyCounts;
}

// 全体のデータ構造
export interface SongData {
    song_count: SongCountEntry;
    diff_count: DifficultyCounts;
}

// マッピング後の楽曲情報
export interface Song {
    level: number;
    Expert?: number;
    Master?: number;
    Append?: number;
}

// マッピング後の全体データ構造
export interface SongInfoData {
    songs: Song[];
    diffCount: DifficultyCounts;
}
