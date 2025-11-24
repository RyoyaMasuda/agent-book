"use client";

import React, { useState } from 'react';
import { WorkflowInstructions } from './components/WorkflowInstructions';
import { WorkflowForm } from './components/WorkflowForm';
import { WorkflowFormData, WorkflowResult } from './types/workflow';
import { WorkflowResults } from './components/WorkflowResults';


const Page = () => {

  const [formData, setFormData] = useState<WorkflowFormData>(
    {
      query:"",
      owner:"",
      repo:""
    }
  )
  
  const [isLoading, setIsLoading] = useState(false);

  const [result, setResult] = useState<WorkflowResult | null>(null); 
  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const {name, value} = e.target;
    setFormData((prev) => {
      return {
        ...prev,
        [name]: value
        // prevの要素を上書きしている。
        // 例えば、const name = query const value = "AIについての情報" の場合、
        // 以前のprevのqueryプロパティの値(例えば"")をAIについての情報で上書きしている。
      }
    })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setResult(null);

    try {
      const response = await fetch("api/workflow/execute", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      })
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult(
        {
          success: false,
          message: "ワークフローの実行中にエラーが発生しました",
          error: error instanceof Error ? error.message : "不明なエラー",
          confluencePages: [],
          githubIssues: [],
          steps: []
        }
      )
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br
     from-blue-50 via-white to-purple-50">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="bg-white/90 backdrop-blur-sm
           rounded-2xl shadow-xl border border-gray-100
            p-8 transition-all hover:shadow-2xl">
            <h1 className="text-3xl font-bold
             bg-gradient-to-r from-blue-600
              to-purple-600 bg-clip-text
               text-transparent mb-8">
              要件書→プロダクトバックログ ワークフロー
            </h1>

            {/* ワークフローの説明と手順を表示するコンポーネント */}
            <div className="mb-8">
              <WorkflowInstructions />
            </div>

            {/* ワークフローのフォームコンポーネント */}
            <WorkflowForm
              formData={formData}
              isLoading={isLoading}
              onInputChange={handleInputChange}
              onSubmit={handleSubmit}
            />

            {/* ワークフローの結果を表示するコンポーネント */}
            <WorkflowResults result={result} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Page;