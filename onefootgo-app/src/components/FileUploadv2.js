'use client'
import React, { useState } from 'react';
import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
import { Upload } from 'lucide-react';
import Image from 'next/image';

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
      Key: `input-videos/${file.name}`,
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
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md p-8 bg-white rounded-lg shadow-md">
        <div className="mb-6">
          <div className="flex justify-center">
            <Image
              src="/logo-light.png"
              alt="OneFootGo Logo"
              width={200}
              height={100}
              objectFit="contain"
            />
          </div>
        </div>
        
        <h1 className="text-black text-2xl font-bold text-center mb-4">Welcome to the OneFootGo Demo!</h1>
        <p className="text-black text-center mb-6">Upload a video file of you being active below</p>
        
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
          <input
            type="file"
            onChange={handleFileChange}
            className="hidden"
            id="file-upload"
          />
          <label
            htmlFor="file-upload"
            className="cursor-pointer flex flex-col items-center justify-center"
          >
            <Upload size={48} className="text-gray-400 mb-2" />
            <span className="text-gray-600">
              {file ? file.name : 'Upload'}
            </span>
          </label>
        </div>
        
        <button
          onClick={uploadFile}
          className="mt-4 w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition duration-200"
        >
          Upload to S3
        </button>
      </div>
    </div>
  );
}