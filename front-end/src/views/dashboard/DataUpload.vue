<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="16"
        ><div class="grid-content ep-bg-purple" />
        数据控制中心
      </el-col>
      <el-col :span="8"
        ><div class="grid-content ep-bg-purple" />
        <el-button type="primary">上传数据</el-button>
      </el-col>
    </el-row>
    <div class="container">
      <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="id" label="#"> </el-table-column>
        <el-table-column prop="name" label="名称"> </el-table-column>
        <el-table-column prop="size" label="大小"> </el-table-column>
        <el-table-column prop="date" label="创建日期"> </el-table-column>
        <el-table-column prop="operation" label="操作"> </el-table-column>
      </el-table>
    </div>
    <el-upload
      ref="upload"
      :action="uploadUrl"
      :on-change="handleChange"
      :on-progress="handleProgress"
      :on-success="handleSuccess"
      :on-error="handleError"
      :before-upload="beforeUpload"
      :http-request="customUpload"
      :show-file-list="false"
      drag
      multiple
    >
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
      <div class="el-upload__tip" slot="tip">
        只能上传 .zip/h5 文件，若为zip文件须保证解压后为h5文件。
      </div>
    </el-upload>

    <el-progress
      v-if="progress !== null"
      :percentage="progress"
      :status="progressStatus"
      style="margin-top: 20px"
    ></el-progress>
  </div>
  <el-button
    v-if="isUploading"
    type="danger"
    @click="cancelUpload"
    style="margin-top: 20px"
  >
    取消上传
  </el-button>
</template>

<script>
import { ElMessage } from "element-plus";
import axios from "axios";
import { time } from "echarts";
import { ref, onMounted } from "vue";

export default {
  data() {
    return {
      uploadUrl: import.meta.env.VITE_APP_API_URL + "/api/dataset/upload", // 后端上传接口
      progress: null, // 上传进度
      progressStatus: null, // 进度条状态 (success/error)
      uploadMessage: null, // 上传消息
      messageType: null, // 消息类型 (success/error)
      abortController: null,
      tableData: [],
    };
  },

  created() {
    this.fetchTableData();
  },

  methods: {
    // 获取文件列表
    fetchTableData() {
      axios
        .get(import.meta.env.VITE_APP_API_URL + "/api/dataset/show")
        .then((response) => {
          const data = response.data.data;
          this.tableData = data.map((item, index) => ({
            id: item.id,
            name: item.file_name,
            size: item.file_size,
            date: item.file_create_date,
            operation: ["下载", "删除"],
          }));
        })
        .catch((error) => {
          console.error(error);
        });
    },
    // 自定义上传请求
    customUpload(options) {
      const formData = new FormData();
      this.isUploading = true;
      this.abortController = new AbortController();
      const signal = this.abortController.signal;
      formData.append("file", options.file);

      const config = {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.lengthComputable) {
            const percentage =
              (progressEvent.loaded / progressEvent.total) * 100;
            this.progress = Math.round(percentage);
          }
        },
        signal,
      };

      axios
        .post(this.uploadUrl, formData, config)
        .then((response) => {
          this.handleSuccess(response.data);
        })
        .catch((error) => {
          if (error.name === "CanceledError") {
            ElMessage.error("取消上传!");
          } else {
            this.handleError(error);
          }
        })
        .finally(() => {
          this.resetState();
        });
    },

    // 文件选择变化时触发
    handleChange(file, fileList) {
      console.log("File selected:", file);
    },

    // 上传进度更新时触发
    handleProgress(event, file, fileList) {
      // 这里的进度信息可以通过 event 来获取，但我们已经在 customUpload 中处理了进度
    },

    // 上传成功时触发
    handleSuccess(response) {
      ElMessage({
        message: "数据集上传成功! 若上传的是zip文件，请等待服务器解析。",
        type: "success",
        plain: true,
      });
    },

    // 上传失败时触发
    handleError(error) {
      ElMessage.error("0ops, 数据集上传失败! 0.o");
    },

    // 上传前的钩子函数
    beforeUpload(file) {
      const isLegal = file.type === "application/zip";

      if (!isLegal) {
        ElMessage.error("0.o, 只能上传h5或zip文件!");
        return false;
      }

      return true;
    },
    // 取消上传
    cancelUpload() {
      if (this.abortController) {
        this.abortController.abort();
        this.isUploading = false;
      }
    },
    // 重置状态
    resetState() {
      console.log(12312312);
      this.progress = null;
      this.progressStatus = null;
      this.uploadMessage = null;
      this.messageType = null;
      this.$refs.upload.clearFiles(); // 清除已选文件
      this.abortController = null;
      this.isUploading = false;
    },
  },
};
</script>

<style scoped>
.el-upload-dragger {
  width: 100%;
  height: 150px;
}
</style>
