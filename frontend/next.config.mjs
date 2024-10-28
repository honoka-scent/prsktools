/** @type {import('next').NextConfig} */
const nextConfig = {
    output: 'export',
    images: {
        unoptimized: true,
    },
    // basePath: '/prsktools', // リポジトリ名がユーザー名.github.io/repo-nameの場合
    // assetPrefix: '/prsktools/',

};

export default nextConfig;
