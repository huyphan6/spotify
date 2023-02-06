import React, { useState } from "react";
import axios from "./utils/axios";

const Sample = () => {
  const [sample, setSample] = useState("");
  const [sampleList, setsampleList] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e) => {
    setSample(e.target.value);
  };

  const getSample = () => {
    setLoading(true);
    axios
      .post("/getSample", { sample: sample })
      .then((res) => {
        console.log("it worked");
        console.log(res.data);
        setsampleList(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.log("it failed");
        console.error(err);
        setLoading(false);
      });
  };

  return (
    <div>
        <h1 style={{display: 'flex',  justifyContent:'center', alignItems:'center'}}>Find Samples!</h1>
        <div style={{display: 'flex',  justifyContent:'center', alignItems:'center'}}>
        <input type="text" value={sample} onChange={handleInputChange} />
      <button onClick={getSample}>Get Sample</button>
      </div>
      {loading ? (
        <div>Loading...</div>
      ) : (
        <ul>
          {sampleList.map((track) => (
            <li key={track.id}>{track}</li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Sample;
