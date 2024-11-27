// src/services/ideaGenService.js
import api from './api';

// Function to post data to generate ideas
export const generateIdeas = async (data) => {
    try {
        const response = await api.post('/api/chatgpt/generateIdeas', data);
        return response.data;
    } catch (error) {
        console.error("Error generating ideas:", error);
        throw error;
    }
};
