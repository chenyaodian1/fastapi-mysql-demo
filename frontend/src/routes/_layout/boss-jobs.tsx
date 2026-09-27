import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { Search } from "lucide-react"
import { Suspense, useState } from "react"

import { client } from "@/client/client.gen"
import { DataTable } from "@/components/Common/DataTable"
import PendingItems from "@/components/Pending/PendingItems"
import { columns, type BossJobTableData } from "@/components/BossJobs/columns"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export const Route = createFileRoute("/_layout/boss-jobs")({
  component: BossJobs,
  head: () => ({
    meta: [
      {
        title: "Boss Jobs - FastAPI Template",
      },
    ],
  }),
})

// Define the response type locally until OpenAPI spec is regenerated
interface BossJobsResponse {
  data: BossJobTableData[]
  count: number
}

function getBossJobsQueryOptions(created_time: string | null, job_name: string | null, city_name: string | null) {
  return {
    queryFn: async () => {
      const query: Record<string, string | number> = { skip: 0, limit: 100 }
      if (created_time) query.created_time = created_time
      if (job_name) query.job_name = job_name
      if (city_name) query.city_name = city_name
      const response = await client.get<BossJobsResponse, unknown, false>({
        url: "/api/v1/boss-jobs/",
        query,
        responseType: "json",
        security: [{ scheme: "bearer", type: "http" }],
      })
      return response.data
    },
    queryKey: ["boss-jobs", created_time, job_name, city_name],
  }
}

function BossJobsTableContent({
  created_time,
  job_name,
  city_name,
}: {
  created_time: string | null
  job_name: string | null
  city_name: string | null
}) {
  const { data: jobsData } = useSuspenseQuery(
    getBossJobsQueryOptions(created_time, job_name, city_name)
  )

  if (!jobsData.data || jobsData.data.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center text-center py-12">
        <div className="rounded-full bg-muted p-4 mb-4">
          <Search className="h-8 w-8 text-muted-foreground" />
        </div>
        <h3 className="text-lg font-semibold">No job listings found</h3>
        <p className="text-muted-foreground">Try adjusting your search filters</p>
      </div>
    )
  }

  return <DataTable columns={columns} data={jobsData.data} />
}

function BossJobsTable(props: {
  created_time: string | null
  job_name: string | null
  city_name: string | null
}) {
  return (
    <Suspense fallback={<PendingItems />}>
      <BossJobsTableContent {...props} />
    </Suspense>
  )
}

function BossJobs() {
  const [createdTime, setCreatedTime] = useState("")
  const [jobName, setJobName] = useState("")
  const [cityName, setCityName] = useState("")

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Boss Job Listings</h1>
          <p className="text-muted-foreground">
            Search and filter job listings from Boss Zhipin
          </p>
        </div>
      </div>

      {/* Search Filters */}
      <div className="flex flex-wrap gap-4 items-end">
        <div className="flex flex-col gap-1.5">
          <label htmlFor="created_time" className="text-sm font-medium">
            Created Date
          </label>
          <Input
            id="created_time"
            type="date"
            value={createdTime}
            onChange={(e) => setCreatedTime(e.target.value)}
            className="w-[200px]"
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <label htmlFor="job_name" className="text-sm font-medium">
            Job Name
          </label>
          <Input
            id="job_name"
            type="text"
            placeholder="Search job name..."
            value={jobName}
            onChange={(e) => setJobName(e.target.value)}
            className="w-[200px]"
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <label htmlFor="city_name" className="text-sm font-medium">
            City
          </label>
          <Input
            id="city_name"
            type="text"
            placeholder="City name..."
            value={cityName}
            onChange={(e) => setCityName(e.target.value)}
            className="w-[200px]"
          />
        </div>

        <Button className="mt-auto">
          <Search className="mr-2 h-4 w-4" />
          Search
        </Button>
      </div>

      {/* Results Table */}
      <BossJobsTable
        created_time={createdTime || null}
        job_name={jobName || null}
        city_name={cityName || null}
      />
    </div>
  )
}
