'use client'
import { useState } from 'react';
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";

export default function FileUploadv2() {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const uploadFile = async () => {
    if (!file) {
      alert('Please select a file first!');
      return;
    }

    const s3Client = new S3Client({
      region: process.env.NEXT_PUBLIC_AWS_REGION,
      credentials: {
        accessKeyId: process.env.NEXT_PUBLIC_AWS_ACCESS_KEY_ID,
        secretAccessKey: process.env.NEXT_PUBLIC_AWS_SECRET_ACCESS_KEY,
      },
    });

    const params = {
      Bucket: process.env.NEXT_PUBLIC_S3_BUCKET,
      Key: 'input-videos/${file.name}',
      Body: file,
    };

    try {
      const command = new PutObjectCommand(params);
      await s3Client.send(command);
      alert('File uploaded successfully!');
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error uploading file');
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={uploadFile}>Upload to S3</button>
    </div>
  );
}