import librosa
import numpy as np
import json
import os

def aggregate_features(features):
    agg_features = {
        'mean': np.mean(features, axis=1),
        'std': np.std(features, axis=1),
        'min': np.min(features, axis=1),
        'max': np.max(features, axis=1)
    }
    return agg_features

def get_mfcc(audio_path):
    # Load the audio file
    y, sr = librosa.load(audio_path)
    
    # Extract MFCC features
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    delta_mfcc = librosa.feature.delta(mfccs, mode='nearest')
    delta2_mfcc = librosa.feature.delta(mfccs, order=2, mode='nearest')

    # Aggregate MFCCs for each coefficient over all frames
    agg_mfccs = aggregate_features(mfccs)
    agg_delta_mfcc = aggregate_features(delta_mfcc)
    agg_delta2_mfcc = aggregate_features(delta2_mfcc)

    # Combine MFCC, delta MFCC, and delta-delta MFCC into a 39x4 array
    combined_features = np.hstack([
        np.vstack([agg_mfccs['mean'], agg_mfccs['std'], agg_mfccs['min'], agg_mfccs['max']]),
        np.vstack([agg_delta_mfcc['mean'], agg_delta_mfcc['std'], agg_delta_mfcc['min'], agg_delta_mfcc['max']]),
        np.vstack([agg_delta2_mfcc['mean'], agg_delta2_mfcc['std'], agg_delta2_mfcc['min'], agg_delta2_mfcc['max']])
    ])

    # Flatten the features for this audio file
    MFCCfeatures = combined_features.flatten()
    
    return MFCCfeatures

def get_audio_files_recursive(base_dir):
    audio_files = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.wav'):
                audio_files.append(os.path.join(root, file))
    return audio_files

def process_audio_files(audio_files, output_json_path):

    audio_files = get_audio_files_recursive(audio_dir)
    
    # Initialize a list to hold feature dictionaries
    features_list = []
    
    # Iterate through all audio files
    for audio_file in audio_files:
        features = get_mfcc(audio_file)
        features_dict = {
            "file": audio_file,
            "features": features.tolist()  # Convert numpy array to list for JSON serialization
        }
        features_list.append(features_dict)
    
    # Save the list to a JSON file
    with open(output_json_path, 'w') as f:
        json.dump(features_list, f, indent=4)
    
    print(f"Features for {len(audio_files)} audio files saved to {output_json_path}")

# Example usage
audio_dir = '../audio_processing/meshrep+peking'
audio_files = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith('.wav')]
output_json_path = '../audio_processing/meshrep+peking_features.json'
process_audio_files(audio_files, output_json_path)
