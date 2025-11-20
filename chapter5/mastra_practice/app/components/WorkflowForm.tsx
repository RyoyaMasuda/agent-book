"use client";

import { WorkflowFormData } from "../types/workflow";

interface WorkflowFormProps {
  formData: WorkflowFormData;
  isLoading: boolean;
  onInputChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onSubmit: (e: React.FormEvent) => void;
}

export const WorkflowForm = (
  {
    formData,
    isLoading,
    onInputChange,
    onSubmit
  }: WorkflowFormProps) => {
    const isFormValid = true;
    return (
      <form onSubmit={onSubmit}>
        <div>
          <label htmlFor="query">検索クエリ</label>
          <input type="text" id="query" name="query" 
                //  value={formData.query} ↓エラー回避のために以下
                 value={formData.query}
                 onChange={onInputChange}
                 placeholder="例: AIについての情報"
                 required />
        </div>
        <div>
          <div>
            <label htmlFor="owner">GitHub Owner</label>
            <input type="text" id="owner" name="owner" 
                  value={formData.owner}
                  onChange={onInputChange}
                  placeholder="例: octocat"
                  required />
          </div>
          <div>
            <label htmlFor="repo">Repository</label>
            <input type="text" id="repo" name="repo" 
                  value={formData.repo}
                  onChange={onInputChange}
                  placeholder="例: mastra_practice"
                  required />
          </div>
        </div>
        <div>
          <button type="submit"
                  disabled={!isFormValid || isLoading}>
            ワークフロー実行
          </button>
        </div>
      </form>
    )
}