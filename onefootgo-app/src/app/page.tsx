// file: app/page.tsx
import VideoAnalyzer from '../components/VideoAnalyzer';
import FileUpload from '../components/FileUpload';
import FileUploadv2 from '@/components/FileUploadv2';

export default function Home() {
  return (
    <main>
      <h1>Upload a file of you being active to analyze!</h1>
      <FileUploadv2 />
      <br></br>
    </main>
  );
}