import React from 'react';

const PredictionCard = ({ prediction }) => {
  const { species, confidence, info } = prediction;
  return (
    <div className="bg-white p-6 rounded-lg shadow-md max-w-md mx-auto">
      <h2 className="text-2xl font-semibold mb-2 capitalize">{species.replace(/_/g, ' ')}</h2>
      <p className="mb-4">Confidence: {(confidence * 100).toFixed(1)}%</p>
      {info.common_name && <p><strong>Common Name:</strong> {info.common_name}</p>}
      {info.habitat && <p><strong>Habitat:</strong> {info.habitat}</p>}
      {info.fun_fact && <p><strong>Fun Fact:</strong> {info.fun_fact}</p>}
    </div>
  );
};

export default PredictionCard;