<template>
    <div class="file-upload">
        <input id="file-input" class="file-upload-label" type="file" @change="handleFileUpload" /></input>
        <button @click="uploadFile" class="upload-button">Upload Selected File</button>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: "Upload",
    data() {
        return {
            file: null
        };
    },
    methods: {
        handleFileUpload(event) {
            this.file = event.target.files[0];
        },
        uploadFile() {
            if (this.file) {
                const formData = new FormData();
                formData.append('file', this.file);

                axios.post('http://localhost:5000/upload', formData)
                    .then(response => {
                        console.log('File uploaded successfully');
                    })
                    .catch(error => {
                        console.error('File upload failed:', error);
                    });
            }
            else {
                console.error('File upload failed:', error);
            }
        },
    },
    mounted() {
        this.uploadFile(); //在加载时自动上传文件
    },
};
</script>

<style>
.file-upload {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 350px;
    margin-bottom: 400px;
    font-size: 16px;
}

.file-upload-label {
    padding: 10px 20px;
    background-color: #122d4f;
    color: #fff;
    border-radius: 5px;
    cursor: pointer;
}

.file-upload-label:hover {
    background-color: #2980b9;
}

.upload-button {
    margin-left: 150px;
    padding: 10px 65px;
    background-color: #122d4f;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
}

.upload-button:hover {
    background-color: #2980b9;
}
</style>