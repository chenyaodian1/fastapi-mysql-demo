import type { ColumnDef } from "@tanstack/react-table"

import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"

// Type for BossJobDetails from API - will be auto-generated
export interface BossJobDetailsPublic {
  id: number
  encrypt_job_id: string
  job_name: string
  salary_desc: string | null
  city_name: string | null
  area_district: string | null
  business_district: string | null
  job_degree: string | null
  job_experience: string | null
  brand_name: string | null
  brand_stage_name: string | null
  brand_industry: string | null
  boss_name: string | null
  boss_title: string | null
  skills: string | null
  welfare_list: string | null
  job_labels: string | null
  created_time: string | null
  boss_online: boolean | null
}

export type BossJobTableData = BossJobDetailsPublic

export const columns: ColumnDef<BossJobTableData>[] = [
  {
    accessorKey: "id",
    header: "ID",
    cell: ({ row }) => (
      <span className="font-mono text-xs text-muted-foreground">
        {row.original.id}
      </span>
    ),
  },
  {
    accessorKey: "job_name",
    header: "Job Name",
    cell: ({ row }) => (
      <span className="font-medium">{row.original.job_name}</span>
    ),
  },
  {
    accessorKey: "salary_desc",
    header: "Salary",
    cell: ({ row }) => (
      <Badge variant="outline" className="font-medium">
        {row.original.salary_desc || "N/A"}
      </Badge>
    ),
  },
  {
    accessorKey: "city_name",
    header: "City",
    cell: ({ row }) => row.original.city_name || "N/A",
  },
  {
    accessorKey: "brand_name",
    header: "Company",
    cell: ({ row }) => row.original.brand_name || "N/A",
  },
  {
    accessorKey: "brand_stage_name",
    header: "Stage",
    cell: ({ row }) => (
      <span
        className={cn(
          "text-muted-foreground",
          !row.original.brand_stage_name && "italic"
        )}
      >
        {row.original.brand_stage_name || "N/A"}
      </span>
    ),
  },
  {
    accessorKey: "boss_name",
    header: "Recruiter",
    cell: ({ row }) => {
      const name = row.original.boss_name
      const title = row.original.boss_title
      return (
        <div className="flex flex-col">
          <span className="font-medium">{name || "N/A"}</span>
          {title && (
            <span className="text-xs text-muted-foreground">{title}</span>
          )}
        </div>
      )
    },
  },
  {
    accessorKey: "boss_online",
    header: "Online",
    cell: ({ row }) => (
      <span
        className={cn(
          "size-2 rounded-full inline-block",
          row.original.boss_online ? "bg-green-500" : "bg-gray-400"
        )}
      />
    ),
  },
  {
    accessorKey: "created_time",
    header: "Created",
    cell: ({ row }) => row.original.created_time || "N/A",
  },
]
