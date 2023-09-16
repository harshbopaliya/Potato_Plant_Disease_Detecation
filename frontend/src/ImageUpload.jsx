import { useState, useEffect } from "react";
import axios from "axios";

const ImageUpload = () => {
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);

    const previewURL = URL.createObjectURL(selectedFile);
    setImagePreview(previewURL);
  };

  const handleSubmit = async () => {
    if (file) {
      const formData = new FormData();

      formData.append("file", file);

      try {
        const response = await axios.post(
          "http://localhost:8000/predict",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        setResponse(response.data);
        console.log(response.data);
      } catch (error) {
        console.error("Error uploading image: ", error);
      } finally {
        isLoading(false);
      }
    }
  };

  useEffect(() => {
    // Simulate a 3-second loading delay
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 3000);

    // Clear the timer when the component unmounts
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className=" p-4  ">
      <div className=" mx-auto  p-4 border rounded-lg shadow-2xl  bg-white/40  text-white">
        <p className=" text-center text-[#68B984] font-semibold text-4xl mb-4">
          HealthyHarvests
        </p>
        <h2 className="text-xl font-semibold mb-4 text-black">
          Upload an Image
        </h2>
        {imagePreview && (
          <div className="mb-4">
            <img
              src={imagePreview}
              alt="Image Preview"
              className=" w-36 h-36"
            />
          </div>
        )}
        <div className="flex items-center ">
          <div className="flex">
            <label
              htmlFor="fileInput"
              className="mb-2 block text-gray-600 cursor-pointer"
            >
              <div className="bg-red-500 text-white px-4 py-2 rounded">
                Upload Image
              </div>
              <input
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                id="fileInput"
                className="hidden"
              />
            </label>
            <div>
              <button
                onClick={handleSubmit}
                className="bg-blue-500 text-white px-4 py-2 rounded ml-4"
              >
                Detect Disease
              </button>
            </div>
          </div>
        </div>

        {response && (
          <div className="mt-4 flex justify-between ">
            <div className="mb-2 border-b p-3 border-2 rounded-lg mx-3 flex flex-col text-black bg-[#A8DF8E] items-center">
              <p className=" font-semibold text-xl mb-2">Detected Disease:</p>
              <p>{response.class}</p>
            </div>
            <div className="mb-2 border-b p-3 border-2 rounded-lg mx-3 flex flex-col text-black bg-[#A8DF8E] items-center">
              <p className=" font-semibold text-xl mb-2">Confidence:</p>
              <p>{response.confidence.toFixed(2) * 100}%</p>
            </div>
            <div className="mb-2 border-b p-3 border-2 rounded-lg mx-3 flex flex-col text-black bg-[#A8DF8E] items-center">
              <p className=" font-semibold text-xl mb-2">Description:</p>
              <p>{response.description}</p>
            </div>
            <div className="mb-2 border-b p-3 border-2 rounded-lg mx-3 flex flex-col text-black bg-[#A8DF8E] items-center">
              <p className=" font-semibold text-xl mb-2">Symptoms:</p>
              <p>{response.symptoms}</p>
            </div>
            <div className="mb-2 border-b p-3 border-2 rounded-lg mx-3 flex flex-col text-black bg-[#A8DF8E] items-center">
              <p className=" font-semibold text-xl mb-2">Causes:</p>
              <p>{response.causes}</p>
            </div>
            <div className="mb-2 border-b p-3 border-2 rounded-lg mx-3 flex flex-col text-black bg-[#A8DF8E] items-center ">
              <p className=" font-semibold text-xl mb-2">Treatments:</p>
              <p>{response.treatments}</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ImageUpload;
