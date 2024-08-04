'use client'
// components/FileUpload.js
import { useState } from 'react';
import AWS from 'aws-sdk';

const S3_BUCKET = process.env.NEXT_PUBLIC_S3_BUCKET;
const REGION = process.env.NEXT_PUBLIC_AWS_REGION;

AWS.config.update({
  accessKeyId: process.env.NEXT_PUBLIC_AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.NEXT_PUBLIC_AWS_SECRET_ACCESS_KEY,
  region: REGION,
});

const FileUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [processedVideoUrl, setProcessedVideoUrl] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleFileInput = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const uploadFile = async (file) => {
    setIsUploading(true);
    const s3 = new AWS.S3();
    const params = {
      Bucket: S3_BUCKET,
      Key: `input-videos/${file.name}`,
      Body: file,
    };

    try {
      const data = await s3.upload(params).promise();
      console.log('File uploaded successfully:', data.Location);
      await processVideo(file.name);
    } catch (err) {
      console.error('Error uploading file:', err);
    } finally {
      setIsUploading(false);
    }
  };

  const processVideo = async (filename) => {
    setIsProcessing(true);
    try {
      const response = await fetch('/api/analyze-video', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ filename }),
      });
      const result = await response.json();
      if (response.ok) {
        setProcessedVideoUrl(`https://${S3_BUCKET}.s3.${REGION}.amazonaws.com/${result.output_file}`);
      } else {
        throw new Error(result.error || 'Failed to process video');
      }
    } catch (error) {
      console.error('Error processing video:', error);
      alert('Failed to process video. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileInput} accept="video/*" />
      <button 
        onClick={() => uploadFile(selectedFile)} 
        disabled={!selectedFile || isUploading || isProcessing}
      >
        {isUploading ? 'Uploading...' : isProcessing ? 'Processing...' : 'Upload'}
      </button>
      {processedVideoUrl && (
        <div>
          <h3>Processed Video:</h3>
          <video src={processedVideoUrl} controls />
        </div>
      )}
    </div>
  );
};

export default FileUpload;